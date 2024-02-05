<script setup>
import { ref } from 'vue'
const q = (s, root) => (root ? root.querySelector(s) : document.querySelector(s))
const msg = '本日のスコア'
const game = ref({})
const members = ref([])
const spinner0 = ref(false)
const spinner1 = ref(false)
const fetchData = () => {
  if (!q('#url').value) {
    alert('SET URL')
    return
  }
  const apiUrl = 'http://localhost:5000/get'
  spinner0.value = true
  members.value.splice(0, members.value.length)
  fetch(apiUrl, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({
      url: q('#url').value,
    }),
  })
    .then((response) => {
      return response.json()
    })
    .then((data) => {
      console.log(data)
      game.value.course = data.course
      game.value.date = new Date(data.date)
      if (data.status === 'error') {
        throw new Error(data['reason'])
      }
      data['scores'].forEach((e) => {
        members.value.push(e)
      })
      setNet()
      spinner0.value = false
    })
    .catch((e) => {
      console.error(e)
      alert(e)
    })
    .finally(() => {
      spinner0.value = false
    })
}

const setNet = () => {
  members.value.forEach((e, i) => {
    members.value[i]['net'] = members.value[i]['gross']
  })
}
function dragList(e, i) {
  console.log(e, i)
  console.log(members.value)
}

function change(e, i, nearPinIndex) {
  if (nearPinIndex === 0) members.value[i].near0 = true
  if (nearPinIndex === 1) members.value[i].near1 = true
  if (nearPinIndex === 2) members.value[i].near2 = true
  if (nearPinIndex === 3) members.value[i].near3 = true
}

const sort = () => {
  members.value.sort((a, b) => {
    if (a.net > b.net) return 1
    if (a.net < b.net) return -1
    return 0
  })
}

const dragIndex = ref(null)

const dragStart = (index) => {
  console.log('drag start', index)
  dragIndex.value = index
}

const hdcp = (i) => {
  members.value[i].net = members.value[i].gross - members.value[i].hdcp
}

const dragEnter = (index) => {
  if (index === dragIndex) return
  const deleteElement = members.value.splice(dragIndex.value, 1)[0]
  members.value.splice(index, 0, deleteElement)
  dragIndex.value = index
}

function send() {
  console.log(members.value)
  if (!confirm('送信してよいですか？')) return
  const apiUrl = 'http://localhost:5000/store'
  spinner1.value = true
  fetch(apiUrl, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({
      course: game.value.course,
      date: game.value.date,
      par: game.value.par,
      scores: members.value,
    }),
  })
    .then((response) => {
      return response.json()
    })
    .then((data) => {
      console.log(data)
      if (data.status === 'error') {
        throw new Error(data['reason'])
      }
    })
    .catch((e) => {
      console.error(e)
      alert(e)
    })
    .finally(() => {
      spinner1.value = false
    })
}
const today = new Date()
</script>
<template>
  <div>
    <h1 class="green">スコア編集</h1>
    <div class="form-group row">
      <div class="col">
        <input class="form-control" type="url" id="url" placeholder="本日のスコアのURL" autofocus />
      </div>
      <div class="col">
        <button class="btn btn-primary" @click="fetchData" :disabled="spinner0">データ取得</button>
      </div>
      <div class="col">
        <div v-show="spinner0" class="spinner-border text-secondary" role="status" />
      </div>
    </div>
    <p>やること：</p>
    <ol>
      <li>名前修正</li>
      <li>ニアピン設定</li>
      <li>HDCP入力</li>
      <li>ソート</li>
    </ol>
    <hr />
    <h2 v-if="game.date" class="green">
      {{ game.course }} {{ game.date.getFullYear() }}/{{ game.date.getMonth() + 1 }}/{{ game.date.getDate() }}
    </h2>
    <table class="table table-striped table-bordered">
      <thead>
        <tr>
          <th>順位</th>
          <th>name</th>
          <th>ニアピン1-9</th>
          <th>ニアピン10-18</th>
          <th>gross</th>
          <th>HDCP</th>
          <th>NET</th>
          <th>獲得ポイント</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="(member, index) in members"
          :draggable="true"
          @dragstart="dragStart(index)"
          @dragenter="dragEnter(index)"
        >
          <td>{{ index + 1 }}</td>
          <td>
            <input class="form-control responsive" type="text" style="min-width: 10em" v-model="member.name" />
          </td>
          <td>
            <input type="checkbox" @change="change(e, index, 0)" v-model="members[index].near0" />
            <input type="checkbox" @change="change(e, index, 1)" v-model="members[index].near1" />
          </td>
          <td class="col-xs-6">
            <input type="checkbox" @change="change(e, index, 2)" :checked="members[index].near2" />
            <input type="checkbox" @change="change(e, index, 3)" :checked="members[index].near3" />
          </td>
          <td>{{ member.gross }}</td>
          <td class="col-lg-2">
            <input
              class="form-control"
              style="min-width: 4em"
              type="number"
              v-model="member.hdcp"
              step="0.1"
              @input="hdcp(index)"
            />
          </td>
          <td>{{ member.net }}</td>
          <td>
            <input style="min-width: 4em" class="form-control col-xs-6" type="number" v-model="member.point" step="1" />
          </td>
        </tr>
      </tbody>
    </table>
    <div class="form-group row">
      <div class="col">
        <button class="btn btn-success" @click="sort">ソート</button>
      </div>
      <div class="col">
        <button class="btn btn-primary" @click="send" :disabled="spinner1">送信</button>
      </div>
      <div class="col">
        <div v-show="spinner1" class="spinner-border text-secondary" role="status" />
      </div>
    </div>
  </div>
</template>

<style scoped>
h1 {
  font-weight: 500;
  font-size: 2.6rem;
  position: relative;
  top: -10px;
}

h3 {
  font-size: 1.2rem;
}

.greetings h1,
.greetings h3 {
  text-align: center;
}
th,
td {
  white-space: nowrap;
}
@media (min-width: 1024px) {
  .greetings h1,
  .greetings h3 {
    text-align: left;
  }
}
h1 {
  margin-top: 0.5em;
}
</style>

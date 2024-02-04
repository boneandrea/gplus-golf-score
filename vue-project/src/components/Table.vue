<script setup>
 import { ref } from 'vue'
 const msg="本日のスコア"
 const members=ref([])
 const fetchData=()=>{
     const url="http://localhost:5000/"
     fetch(url).then((response) => {
         console.log(response.status)
         return response.json()
     }).then((data) => {
         console.log(data)
         if(data.status=== "error"){
             throw new Error(data["reason"])
         }
         data["scores"].forEach(e=>{
             members.value.push(e)
         })
     }).catch(e=>{
         console.error(e)
         alert(e)
     })
 }
 fetchData()
 // init
 members.value.forEach((e,i)=>{
     members.value[i].point=90-i
     members.value[i].hdcp=36-i*0.5
     members.value[i].gross=i+80
     members.value[i].net=members.value[i].gross-members.value[i].hdcp
 })

 function dragList(e,i){
     console.log(e,i)
     console.log(members.value)
 }

 function change(e,i,nearPinIndex){
     if(nearPinIndex===0) members.value[i].near0=true
     if(nearPinIndex===1) members.value[i].near1=true
     if(nearPinIndex===2) members.value[i].near2=true
     if(nearPinIndex===3) members.value[i].near3=true
 }

 const dragIndex = ref(null);

 const dragStart = (index) => {
     console.log('drag start', index)
     dragIndex.value = index
 }

 const hdcp=(i)=>{
     console.log(members.value[i].hdcp)
     members.value[i].net=
         members.value[i].gross-members.value[i].hdcp
 }

 const dragEnter = (index) => {
     if (index === dragIndex) return
     const deleteElement = members.value.splice(dragIndex.value, 1)[0]
     members.value.splice(index, 0, deleteElement)
     dragIndex.value = index
 }

 function send(){
     console.log(members.value)
     if(confirm("送信してよいですか？"))
         console.log(members.value[3].name)
     console.log(JSON.stringify(members.value))
     alert("sent")
 }
 const today=new Date()
</script>
<template>
    <div>
        <h1 class="green">
            スコア編集:{{today.getFullYear()}}/{{today.getMonth()+1}}/{{today.getDate()}}
            <button class="btn btn-primary btn-lg" @click="send">送信</button>
        </h1>
        <h2>
            入力するもの：
        </h2>
        <ul>
            <li>HDCP</li>
            <li>ニアピン</li>
        </ul>
        <hr>
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
                <tr v-for="(member,index) in members"
                    :draggable="true"
                    @dragstart="dragStart(index)"
                    @dragenter="dragEnter(index)"
                >
                    <td>{{index+1}}</td>
                    <td>{{member.name}}</td>
                    <td>
                        <input type="checkbox"
                               @change="change(e,index,0)"
                               :checked="members[index].near0"
                        />
                        <input type="checkbox"
                               @change="change(e,index,1)"
                               :checked="members[index].near1"
                        />
                    </td>
                    <td class="col-xs-6">
                        <input type="checkbox"
                               @change="change(e,index,2)"
                               :checked="members[index].near2"
                        />
                        <input type="checkbox"
                               @change="change(e,index,3)"
                               :checked="members[index].near3"
                        />
                    </td>
                    <td>{{member.gross}}</td>
                    <td class="col-lg-2">
                        <input class="form-control col-xs-6"
                               type="number" v-model="member.hdcp" step="0.1"
                               @input="hdcp(index)"/>
                    </td>
                    <td> {{member.net}} </td>
                    <td>{{member.point}}</td>
                </tr>
            </tbody>
        </table>
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
 th,td{ white-space: nowrap; }
 @media (min-width: 1024px) {
     .greetings h1,
     .greetings h3 {
         text-align: left;
     }
 }
 h1{
     margin-top:0.5em;
 }
</style>

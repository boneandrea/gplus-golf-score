/*!
* Start Bootstrap - Freelancer v7.0.7 (https://startbootstrap.com/theme/freelancer)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-freelancer/blob/master/LICENSE)
*/
//
// Scripts
//

window.addEventListener('DOMContentLoaded', event => {

    // Navbar shrink function
    var navbarShrink = function () {
        const navbarCollapsible = document.body.querySelector('#mainNav');
        if (!navbarCollapsible) {
            return;
        }
        if (window.scrollY === 0) {
            navbarCollapsible.classList.remove('navbar-shrink')
        } else {
            navbarCollapsible.classList.add('navbar-shrink')
        }

    };

    // Shrink the navbar
    navbarShrink();

    // Shrink the navbar when page is scrolled
    document.addEventListener('scroll', navbarShrink);

    // Activate Bootstrap scrollspy on the main nav element
    const mainNav = document.body.querySelector('#mainNav');
    if (mainNav) {
        new bootstrap.ScrollSpy(document.body, {
            target: '#mainNav',
            rootMargin: '0px 0px -40%',
        });
    };

    // Collapse responsive navbar when toggler is visible
    const navbarToggler = document.body.querySelector('.navbar-toggler');
    const responsiveNavItems = [].slice.call(
        document.querySelectorAll('#navbarResponsive .nav-link')
    );
    responsiveNavItems.map(function (responsiveNavItem) {
        responsiveNavItem.addEventListener('click', () => {
            if (window.getComputedStyle(navbarToggler).display !== 'none') {
                navbarToggler.click();
            }
        });
    });
});

const setAppendValue=()=>{
    document.querySelectorAll("tbody tr").forEach(tr=>{
        let score=0
        const prize_td=tr.querySelectorAll("td")[4]
        const prize=prize_td.innerText

        const holeIneOne=prize.match(/ホールインワン (\d+)/)
        if(holeIneOne){
            score+=parseInt(holeIneOne[1])*10000
        }
        const albatross=prize.match(/アルバトロス (\d+)/)
        if(albatross){
            score+=parseInt(albatross[1])*1000
        }
        const eagle=prize.match(/イーグル (\d+)/)
        if(eagle){
            score+=parseInt(eagle[1])*100
        }
        const birdie=prize.match(/バーディ (\d+)/)
        if(birdie){
            score+=parseInt(birdie[1])
        }
        prize_td.className=`{sortValue: ${score}}`
    })
}

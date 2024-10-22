document.addEventListener("DOMContentLoaded", () => {
    const tabs = Array.from(document.getElementsByClassName('tab'))
    const wrap_divs = Array.from(document.getElementsByClassName('wrap'))
    tabs.forEach(e => {
        e.addEventListener("click", () => {
            document.querySelector('.selected').classList.toggle('selected')
            e.classList.toggle('selected')

            if (e.id == '1') {
                wrap_divs[0].classList.toggle('unactive')
                wrap_divs[1].classList.toggle('unactive')
            }
            else {
                wrap_divs[1].classList.toggle('unactive')
                wrap_divs[0].classList.toggle('unactive')
            }
        })
    })

})
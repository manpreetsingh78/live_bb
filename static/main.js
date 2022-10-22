console.log("Hello ")

const url = window.location.href

const searchform = document.getElementById('search-form')
const searchinput = document.getElementById('search-input')
const resultbox = document.getElementById('results-box')
const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value

const lat = document.getElementById('lat')
const long = document.getElementById('long')

const sendsearchdata = (game) => {
    $.ajax({
        type: 'POST',
        url: 'search/',
        data: {
            'csrfmiddlewaretoken':csrf,
            'game':game
        },
        success:(res) =>{
            console.log(res.data)
            const data = res.data
            resultbox.innerHTML = ""
            if (Array.isArray(data)) {
                data.forEach(game => {
                    resultbox.innerHTML += `<option id=${game.pk}>${game.address}</option>`
                    searchinput.innerHTML = `${game.address}`
                    lat.value = `${game.lat}`
                    long.value = `${game.long}`
                })
                


                }else{
                    if (searchinput.value.length > 0) {
                        console.log("1st else")
                        resultbox.innerHTML = `<b>${data}</b>`
                    }else{
                        console.log("2nd else")
                        resultbox.classList.add('not-visible')
                    }
                }
        },
        error:(err) =>{
            console.log(err)
        }
    })

}

searchinput.addEventListener('keyup',e => {
    console.log(e.target.value)
    if (resultbox.classList.contains('not-visible')){
        resultbox.classList.remove('not-visible')
    }

    sendsearchdata(e.target.value)
})








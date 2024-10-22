const button = document.querySelector('.subscribe_button')
const fetch_URL = "/api/v1/follow"
const username = document.querySelector('.profile_username').innerText

const csrf_token = getCookies().csrftoken

fetch(fetch_URL + "?" + new URLSearchParams({
        username: username,
        purpose: "is_following"
    }))
    .then(response => response.json())
    .then(data => {
        if (data.is_following == true){
            button.innerText = "Отписаться"
        }
        else {
            button.innerText = "Подписаться"
        }
    })

button.addEventListener("click", () => {
    var action = button.dataset.action
    fetch(fetch_URL, {
        method: "POST",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token,
        },
        body: JSON.stringify({
            username: username,
            action: action
        })
    })
        .then(response => response.json())
        .then(data => {
                if (action == "follow")
                {
                    button.dataset.action = "unfollow"
                    button.innerText = "Отписаться"
                }
                else
                {
                    button.dataset.action = "follow"
                    button.innerText = "Подписаться"
                }
                const followers_count = document.querySelector('.followers_count_text')
                followers_count.innerText=data.followers_count
        })
})
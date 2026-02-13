const submit_button = document.getElementById("btn_send")
const chat_input = document.getElementById("chat_input")
const chat_scrollable = document.getElementById("chatContainer")

submit_button.addEventListener("click", send_message)

async function send_message(event) {
    event.preventDefault()

    const user_input = chat_input.value
    chat_input.value = ""
    if (user_input) {

        newChatMessage(user_input, "User")
        submit_button.disabled = true

        const data = {"question": user_input}

        try {
            let httpResponse = await fetch("http://localhost:8000/api/query", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(data)
            })
            
            // Get raw text first to see what we're receiving
            let rawText = await httpResponse.text()
            
            // Parse it as JSON
            let response = JSON.parse(rawText)

            newChatMessage(response["answer"], "Assistant")
        } catch (error) {
            newChatMessage("Error: Failed to get response", "Assistant")
            console.error(error)
        } finally {
            submit_button.disabled = false
        }
    }

}

function newChatMessage(message, user){
    const new_message = document.createElement('div')
    if (user == "User"){
        new_message.classList.add("messageUser")
        new_message.textContent = message
    } else {
        new_message.classList.add("messageAssistant")
        new_message.innerHTML = marked.parse(message)
    }
    chat_scrollable.appendChild(new_message)
    chat_scrollable.scrollTop = chat_scrollable.scrollHeight
}


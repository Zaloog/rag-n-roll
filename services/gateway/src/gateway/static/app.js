const submit_button = document.getElementById("btn_send")
const chat_input = document.getElementById("chat_input")
const chat_scrollable = document.getElementById("chatContainer")
const upload_button = document.getElementById("uploadBtn")
const file_input = document.getElementById("fileInput")
const upload_status = document.getElementById("uploadStatus")

submit_button.addEventListener("click", send_message)
upload_button.addEventListener("click", upload_files)

async function send_message(event) {
    event.preventDefault()

    const user_input = chat_input.value
    chat_input.value = ""
    if (user_input) {

        newChatMessage(user_input, "User")
        submit_button.disabled = true

        const data = {"question": user_input}

        try {
            startSpinner()
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
            stopSpinner()
            
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

function startSpinner() {
    const spinner = document.querySelector(".spinner")
    if (spinner == null) {
        const spinner = document.createElement('div')
        spinner.classList.add("spinner")
        chat_scrollable.appendChild(spinner)
    }
}

function stopSpinner() {
    const spinner = document.querySelector(".spinner")
    if (spinner) spinner.remove()
}

async function upload_files(event) {
    const files = file_input.files
    // const files = event.target.files
    
    if (!files || files.length === 0) {
        return
    }
    
    upload_status.textContent = `Uploading ${files.length} file(s)...`
    upload_status.className = "status-uploading"
    upload_button.disabled = true
    
    const formData = new FormData()
    for (let i = 0; i < files.length; i++) {
        formData.append('files', files[i])
    }
    
    try {
        let httpResponse = await fetch("http://localhost:8000/api/upload", {
            method: "POST",
            body: formData
        })
        
        if (!httpResponse.ok) {
            throw new Error(`Upload failed: ${httpResponse.statusText}`)
        }
        
        let response = await httpResponse.json()
        
        upload_status.textContent = `✓ Successfully uploaded and processed ${response.documents_processed} document(s)`
        upload_status.className = "status-success"
        
        // Clear file input
        file_input.value = ""
        
        // Clear status after 5 seconds
        setTimeout(() => {
            upload_status.textContent = ""
            upload_status.className = ""
        }, 5000)
        
    } catch (error) {
        upload_status.textContent = `✗ Upload failed: ${error.message}`
        upload_status.className = "status-error"
        console.error("Upload error:", error)
    } finally {
        upload_button.disabled = false
    }
}

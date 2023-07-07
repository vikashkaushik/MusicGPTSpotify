import "https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"


const API_KEY = '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'
const submitButton = document.querySelector('#submit')
const outPutElement = document.querySelector('#output')
const inputElement = document.querySelector('input')
const historyElement = document.querySelector('.history')
const buttonElement = document.querySelector('button')
function changeInput(value){
    const inputElement = document.querySelector('input')
    inputElement.value = value;
}

async function getMessage(){

    $.ajax({
        url: '/getMessage',
        type: 'POST',
        data: { 'input': inputElement.textContent},
        success: function(response){
            outPutElement.textContent = response;
        },
        error: function(error){
            console.log(error);
        }
    });

    // out = fetch('/getMessage', {
    //     input: inputElement.textContent
    // })
    // .then(response=> response.text())
    // .then(result => {
    //     outPutElement.textContent = result
    // })
    // .catch(error=> {
    //     console.error(error);
    // });

    // console.log('clicked')
    // const options = {
    //     method: 'POST',
    //     headers: {
    //         'Authorization': `Bearer ${API_KEY}`,
    //         'Content-Type': 'application/json'

    //     },
    //     body: JSON.stringify({
    //         model: "gpt-3.5-turbo",
    //         messages: [{role: "user", content: inputElement.value}],
    //         max_tokens: 100
    //     })

    // }

    // try{
    //     const response = await fetch('https://api.openai.com/v1/chat/completions', options)
    //     const data = await response.json()
    //     console.log(data)

    //     if(inputElement.value == "How many liked songs do I have?"){
    //         fetch('/getTracks')
    //         .then(response => response.text())
    //         .then(result => {
    //             // Handle the result in JavaScript
    //             outPutElement.textContent = result
    //         })
    //         .catch(error => {
    //             // Handle any errors
    //             console.error(error);
    //         });
    //     }
    //     else{
    //         outPutElement.textContent = data.choices[0].message.content
    //     }
       
        

    if(outPutElement.textContent && inputElement.value){
        const pElement = document.createElement('p')
        pElement.textContent = inputElement.value
        pElement.addEventListener('click', () => changeInput(pElement.textContent))
        historyElement.append(pElement)
    }
    // } catch (error){
    //     console.error(error)
    // }
}

submitButton.addEventListener('click', getMessage)

function clearInput(){
    inputElement.value = '';
}
buttonElement.addEventListener('click', clearInput)

console.log('cupcakes in the hizzy')

defaultImageUrl = "https://tinyurl.com/demo-cupcake"

$('#new-cupcake-form').submit(function(e) {
    e.preventDefault()
    formData = {}
    for (let i = 0; i < 4; i++) {
        formData[e.target[i].id] = e.target[i].value
    }
    formData.rating = parseFloat(formData.rating)
    if (!formData.image) {
        formData.image = defaultImageUrl
    }
    jsonData = JSON.stringify(formData)
    console.log(jsonData)
    processCupcakeForm(jsonData)
})

async function processCupcakeForm(jsonData) {
    const newCupcake = await axios.post('/api/cupcakes', jsonData)
    console.log(newCupcake)
}
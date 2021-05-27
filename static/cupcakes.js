const defaultImageUrl = "https://tinyurl.com/demo-cupcake";
const apiBaseUrl = "/api/cupcakes";
const $cupcakesDisplay = $('#cupcakes-display')

function displayCupcakesHtml(cupcake) {
    return `
        <div class="col col-md-4 col-lg-3">
            <div class="card card-dark">
                <img src="${cupcake.image}" alt="cupcake picture" class="card-img-top img-fluid">
                <div class="card-body bg-dark">
                    <h4 class="card-title text-light">${cupcake.flavor}</h4>
                    <p class="card-text text-light">
                        size: ${cupcake.size}<br>
                        rating: ${cupcake.rating}
                    </p>
                </div>
            </div>
        </div>
    `;
};

async function getCupcakesFromApi() {
    const apiCupcakes = await axios.get(apiBaseUrl);
    for (let cupcakeData of apiCupcakes.data.cupcakes) {
        let cupcake = $(displayCupcakesHtml(cupcakeData));
        $cupcakesDisplay.append(cupcake);
    }
}

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
    processCupcakeForm(formData);
})

async function processCupcakeForm(formData) {
    const newCupcake = await axios.post(apiBaseUrl, formData);
    $('#new-cupcake-form').trigger("reset");
    displayCupcakesHtml(newCupcake);
}

getCupcakesFromApi();
const defaultImageUrl = "https://tinyurl.com/demo-cupcake"
const APIBaseUrl = "/api/cupcakes"

function displayCupcakeHTML(cupcake) {
    return `
        <div class="col col-md-4 col-lg-3 mb-3">
            <div class="card card-dark">
                <img src="{{ cupcake.image }}" alt="cupcake picture" class="card-img-top img-fluid">
                <div class="card-body bg-dark">
                    <h4 class="card-title text-light">{{ cupcake.flavor }}</h4>
                    <p class="card-text text-light">
                        size: {{ cupcake.size }}<br>
                        rating: {{ cupcake.rating }}
                    </p>
                </div>
            </div>
        </div>
        <div class="col col-md-4 col-lg-3 mb-3">
            <div class="card card-dark">
                <img src="{{ cupcake.image }}" alt="cupcake picture" class="card-img-top img-fluid">
                <div class="card-body bg-dark">
                    <h4 class="card-title text-light">{{ cupcake.flavor }}</h4>
                    <p class="card-text text-light">
                        size: {{ cupcake.size }}<br>
                        rating: {{ cupcake.rating }}
                    </p>
                </div>
            </div>
        </div>
    `;
}

async function loadApiCupcakes() {
    const resp = await axios.get(APIBaseUrl);

    for (let cupcakeData of resp.data.cupcakes) {
        const thisCupcake = $(displayCupcakeHTML(cupcakeData));
        $("#cupcake-display".append(thisCupcake));
    }
}

$('#new-cupcake-form').submit(function(e) {
    e.preventDefault();
    formData = {};
    for (let i = 0; i < 4; i++) {
        formData[e.target[i].id] = e.target[i].value;
    };
    try {
        formData.rating = parseFloat(formData.rating);
    } catch (error) {
        alert('rating must be a number')
    };
    if ((formData.rating < 0) || (formData.rating > 10));
        alert('rating must be between 0 and 10');

        if (!formData.image) {
            formData.image = defaultImageUrl;
    };

    // jsonData = JSON.stringify(formData)
    processCupcakeForm(formData);
})

async function processCupcakeForm(formData) {
    const newCupcakeResponse = await axios.post(APIBaseURL, formData);
    const newCupcake = $(displayCupcakeHTML(newCupcakeResponse.data.cupcake));
    $("#cupcake-display").append(newCupcake);
    $("#new-cupcake-form").trigger("reset");
};

$(loadApiCupcakes)
document.getElementById("predictForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const formData = new FormData(this);
    let data = {};

    formData.forEach((value, key) => {
        data[key] = value;
    });

    const response = await fetch("/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    const result = await response.json();

    if (result.price) {
        document.getElementById("result").innerText = "💰 Price: ₹ " + result.price;
    } else {
        document.getElementById("result").innerText = "❌ Error";
    }
});
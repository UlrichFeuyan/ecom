function ImgUpload() {
    let imgWrap = document.querySelector(".upload__img-wrap");
    let inputFile = document.querySelector(".upload__inputfile");
    let imgArray = [];

    inputFile.addEventListener("change", function (e) {
        let files = e.target.files;
        let maxLength = parseInt(inputFile.getAttribute("data-max_length")) || 20;

        if (files.length + imgArray.length > maxLength) {
            alert("Vous ne pouvez pas télécharger plus de " + maxLength + " images.");
            return;
        }

        Array.from(files).forEach((file) => {
            if (!file.type.startsWith("image/")) return;

            imgArray.push(file);

            let reader = new FileReader();
            reader.onload = function (event) {
                let div = document.createElement("div");
                div.classList.add("upload__img-box");

                let imgDiv = document.createElement("div");
                imgDiv.classList.add("img-bg");
                imgDiv.style.backgroundImage = `url(${event.target.result})`;
                imgDiv.dataset.file = file.name;

                let closeBtn = document.createElement("div");
                closeBtn.classList.add("upload__img-close");
                closeBtn.innerHTML = "&times;";

                closeBtn.addEventListener("click", function () {
                    let fileName = imgDiv.dataset.file;
                    imgArray = imgArray.filter(f => f.name !== fileName);
                    div.remove();
                });

                imgDiv.appendChild(closeBtn);
                div.appendChild(imgDiv);
                imgWrap.appendChild(div);
            };
            reader.readAsDataURL(file);
        });
    });

    document.getElementById("product-form").addEventListener("submit", function (event) {
        let formData = new FormData(this);
        imgArray.forEach((file) => {
            formData.append("images", file);
        });

        fetch(this.action, {
            method: "POST",
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            } else {
                alert("Erreur lors de l’enregistrement.");
            }
        })
        .catch(error => console.error("Erreur:", error));

        event.preventDefault();
    });
}

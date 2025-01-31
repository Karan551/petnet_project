
const initApp = () => {
    console.log("hello world");

    // ---------- To show copyright year
    const currentYear = new Date().getFullYear();

    const year = document.querySelector("#copyright-year");
    year.innerHTML = currentYear + "-" + String((currentYear + 1)).slice(-2);

    // -------------------Prompt user
    const promptUser = document.querySelectorAll(".prompt-user") || [];

    if (promptUser) {
        promptUser.forEach((eachElement) => {
            eachElement.addEventListener("submit", function (event) {
                const confirmUser = confirm("Are you sure to logout ?");
                if (!confirmUser) {
                    event.preventDefault();
                }
            });

        });
    }

    // ------------------- To delete product
    function handleForm(formElement, label) {

        formElement.addEventListener("submit", function (event) {
            const prompt = confirm(`Are you sure to ${label} this product?`);
            if (!prompt) {
                event.preventDefault();
            }

        });

    }
    const deleteForm = document.querySelector("#delete-prod-form") || null;

    if (deleteForm) {

        handleForm(deleteForm, "delete");
    }


    // ------------------- To remove messages
    const msgElement = document.querySelector("#msg-content") || null;

    if (msgElement) {
        const parentContent = msgElement.parentNode;

        setTimeout(() => {
            parentContent.removeChild(msgElement);
        }, 3000);
    }
};


document.addEventListener("DOMContentLoaded", initApp);
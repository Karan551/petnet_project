
const initApp = () => {
    console.log("hello world");

    // ---------- To show copyright year
    const currentYear = new Date().getFullYear();

    // console.log("this is current year::", currentYear);
    // console.log("this is current year::", String((currentYear+1)).slice(-2));

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
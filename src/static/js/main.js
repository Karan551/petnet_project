
const initApp = () => {
    console.log("hello world");

    // ---------- To show copyright year
    const currentYear = new Date().getFullYear();

    console.log("this is current year::", currentYear);
    console.log("this is current year::", String((currentYear+1)).slice(-2));

    const year = document.querySelector("#copyright-year");
    year.innerHTML = currentYear + "-" + String((currentYear+1)).slice(-2);
};


document.addEventListener("DOMContentLoaded", initApp);
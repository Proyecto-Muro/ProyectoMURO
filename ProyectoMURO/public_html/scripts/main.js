
document.addEventListener('DOMContentLoaded', () => {
    if(localStorage.getItem('darkEnabled')=='true'){
	    DarkReader.setFetchMethod(window.fetch);
        DarkReader.enable({brightness: 100, contrast: 150, sepia: 0});
        
    } else {
        DarkReader.disable();
    }
    const toggle = document.querySelector('.switch input');
    toggle.addEventListener('click', () => {
	    const isEnabled = DarkReader.isEnabled();
        if(isEnabled){
            DarkReader.disable();
            localStorage.setItem('darkEnabled', false)
        } else {
            DarkReader.setFetchMethod(window.fetch);
            DarkReader.enable({brightness: 100, contrast: 150, sepia: 0});
            localStorage.setItem('darkEnabled', true)
        }
    })
})


/*
const btn = document.querySelector('.switch input');

const theme = document.querySelector("#theme-link");


btn.addEventListener("click", function() {
if (theme.getAttribute("href") == "/styles/light-theme.css") {

    theme.href = "/styles/dark-theme.css";

} else {

    theme.href = "/styles/light-theme.css";
}
});
*/

function copyEvent(latex) {
    navigator.clipboard.writeText(latex);
    window.getSelection().removeAllRanges();
} 



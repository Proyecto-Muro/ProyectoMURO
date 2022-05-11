
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
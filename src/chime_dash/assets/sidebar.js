const copy_to_clipboard = () => {
    // Copies url to clipboard and changes the button text to let the user know it happened.
    const el = document.createElement('textarea');
    const button = document.getElementById('copy_params');
    let original_text = button.textContent;
    el.value = window.location.href;
    document.body.appendChild(el);
    el.select();
    document.execCommand('copy');
    document.body.removeChild(el);
    button.textContent = "URL copied to clipboard";
    let t = setTimeout(function(button, original_text){button.textContent = original_text;}, 2500, button, original_text);
    return el.value;
};

const reset_parameters = () => {
    // Resets parameters by redirecting to the root url, effectively clearing whatever is in the hash
    window.location = window.location.origin;
}

// Could probably replace this with a jquery-style .ready function
let c = 0;
let dom_ready = setInterval(function(){
    // console.log(c++);
    if( document.getElementById('n_days') != null) {  // assumes n_ready. todo: add that to tests
        clearInterval(dom_ready);
        on_load();
    } else if( c > 200 ){
        clearInterval(dom_ready);  // took over 2 seconds to load the dom... No go.
    }
}, 10);

const on_load = () => {
    /*
    This function is triggered by the interval above.
    It will grab the hash, update the sidebar, and watch for changes to the hash and update the sidebar.
     */
    document.getElementById("copy_params").onclick = copy_to_clipboard;
    document.getElementById("reset_params").onclick = reset_parameters;
};
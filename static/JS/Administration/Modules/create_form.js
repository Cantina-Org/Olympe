var config = 'ee';

function create_form() {
    let files = document.getElementById('file-input').files;
    let modules_name = document.getElementById('modules-name');

    if (files.length !== 0 && modules_name.value === "Autre") {
        let fr = new FileReader();

        fr.onload = async function(e) {
            console.log(e);
            let result = JSON.parse(e.target.result);
            config = JSON.stringify(result, null, 2);
            console.log(config)
        }
        fr.readAsText(files.item(0));
        console.log(config)
    }
}
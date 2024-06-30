function show_file_input(){
    let input = document.getElementById('modules-name')
    document.getElementById('modules-name-file').hidden = input.value !== 'autre';
    console.log(input.value !== 'autre')
    console.log(input.value)
}
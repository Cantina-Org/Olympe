function delete_account(){
    if (confirm('Êtes vous sûr de vouloir supprimer ce compte ?')) {
        let form = document.getElementById('delete_account');
        let input = document.createElement("input");
        input.type = "hidden";
        input.name = 'token_action_author';
        input.value = getCookie('token');
        form.appendChild(input);
        form.submit();
    } else {
        console.log('Annulation de la requete.');
    }
}

function getCookie(name) {
  let match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
  if (match) return match[2];
}
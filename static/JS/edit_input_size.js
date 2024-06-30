function edit_input_size(input) {
    // Récupérer la longueur du texte
    let longueurTexte = input.value.length;

    if (longueurTexte * 10 >= input.style.width) {
        // Ajuster la largeur de l'input en fonction de la longueur du texte
        input.style.width = (longueurTexte * 10) + 'px'; // Vous pouvez ajuster le facteur multiplicatif selon vos besoins
    } else {}
}
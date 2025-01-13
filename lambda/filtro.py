def excluir_labels(labels):
    """Remove labels indesejadas."""
    labels_excluidas = [
        'Food and Beverage', 'Weapons and Military', 'Ammunition',
        'Weapon', 'Bullet', 'Produce', 'Plant',
        'Plants and Flowers', 'Citrus Fruit', "Smoke Pipe", 'Animals and Pets', 'Animal',
        "Sea Life", "Seafood"
    ]
    return [label['Name'] for label in labels if label['Name'] not in labels_excluidas]
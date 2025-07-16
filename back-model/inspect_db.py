from database.crud import get_all_products, get_all_users

def main():
    print("Usuarios:")
    users = get_all_users()
    for u in users:
        print(dict(u))  # Convierte cada fila a dict para imprimir

    print("\nProductos:")
    products = get_all_products()
    for p in products:
        print(dict(p))

if __name__ == "__main__":
    main()

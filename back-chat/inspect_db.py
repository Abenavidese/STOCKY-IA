from database.crud import get_all_messages, get_all_threads

def main():
    print("\nHilos:")
    threads = get_all_threads()
    for t in threads:
        print(dict(t))

    print("\nMensajes:")
    messages = get_all_messages()
    for m in messages:
        print(dict(m))


if __name__ == "__main__":
    main()

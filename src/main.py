import med_manager

def exibir_menu():
    print("\n" + "="*35)
    print("💊 MEDCONTROL - Menu Principal")
    print("="*35)
    print("1. Adicionar Medicamento")
    print("2. Listar Medicamentos")
    print("3. Remover Medicamento")
    print("4. Sair")
    print("="*35)

def main():
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção (1-4): ")

        if opcao == '1':
            print("\n--- Adicionar Medicamento ---")
            nome = input("Nome do medicamento: ")
            dosagem = input("Dosagem (ex: 50mg, 1 comprimido): ")
            horario = input("Horário (ex: 08:00): ")
            
            try:
                med_manager.adicionar_medicamento(nome, dosagem, horario)
                print(f"✅ Medicamento '{nome}' adicionado com sucesso!")
            except ValueError as e:
                print(f"❌ Erro: {e}")

        elif opcao == '2':
            print("\n--- Lista de Medicamentos ---")
            meds = med_manager.listar_medicamentos()
            if not meds:
                print("⚠️ Nenhum medicamento cadastrado no momento.")
            else:
                for i, med in enumerate(meds, 1):
                    print(f"{i}. {med['nome']} | Dosagem: {med['dosagem']} | Horário: {med['horario']}")

        elif opcao == '3':
            print("\n--- Remover Medicamento ---")
            nome = input("Qual o nome do medicamento que deseja remover? ")
            sucesso = med_manager.remover_medicamento(nome)
            if sucesso:
                print(f"✅ '{nome}' removido com sucesso!")
            else:
                print(f"❌ Medicamento '{nome}' não encontrado.")

        elif opcao == '4':
            print("\nSaindo do MedControl... Cuide bem da saúde! 👋\n")
            break

        else:
            print("\n❌ Opção inválida. Digite um número de 1 a 4.")

if __name__ == "__main__":
    main()
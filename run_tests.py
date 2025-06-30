import unittest

def run_todos_os_testes():
    print("=" * 40)
    print("Iniciando execução dos testes".center(40))
    print("=" * 40)

    loader = unittest.TestLoader()
    suite = loader.discover('test')

    runner = unittest.TextTestRunner(verbosity=2)
    resultado = runner.run(suite)

    print("\n" + "=" * 40)
    print("Testes finalizados".center(40))
    print("=" * 40)
    print(f"Total de testes executados: {resultado.testsRun}")
    print(f"Falhas: {len(resultado.failures)} | Erros: {len(resultado.errors)}")
    print("=" * 40)

if __name__ == '__main__':
    try:
        run_todos_os_testes()
    except Exception as e:
        print("Erro inesperado ao rodar os testes:")
        print(e)

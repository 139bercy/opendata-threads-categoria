import eda
import extract_datasets
import extract_discussions
import merging_MEFSIN

import inference

if __name__ == "__main__":
    print("Début de l'exécution de main.py")

    print("\nExécution de 'extract_discussions' depuis main.py :")
    extract_discussions.main()

    print("\nExécution de 'extract_datasets' depuis main.py :")
    extract_datasets.main()

    print("\nExécution de 'merging_MEFSIN' depuis main.py :")
    merging_MEFSIN.main()

    print("\nExécution de 'inference' depuis main.py :")
    inference.main()

    print("\nExécution de 'eda' depuis main.py :")
    # eda.()

    print("\nFin de l'exécution de main.py")

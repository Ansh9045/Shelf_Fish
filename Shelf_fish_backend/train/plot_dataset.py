import os
import matplotlib.pyplot as plt

def get_image_counts(folder):
    counts = {}
    for root, dirs, files in os.walk(folder):
        for file in files:
            class_name = os.path.basename(root)
            counts[class_name] = len(files)
    return counts


if __name__ == "__main__":
    folder = "images"
    counts = get_image_counts(folder)

    plt.bar(counts.keys(), counts.values())
    plt.xlabel('Class')
    plt.ylabel('Number of Images')
    plt.xticks(rotation=45)
    plt.title('Number of Images per Class')
    plt.tight_layout()
    plt.show()
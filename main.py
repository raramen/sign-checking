import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import cv2
from skimage.metrics import structural_similarity as ssim

# from signature import match


# Threshold
T = 74


def match(path1, path2):
    # read the images
    img1 = cv2.imread(path1)
    img2 = cv2.imread(path2)
    # Mengconvert gambar menjadi grayscale
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # turn images to binary
    ret1, binary1 = cv2.threshold(img1, 127, 255, cv2.THRESH_BINARY)
    ret2, binary2 = cv2.threshold(img2, 127, 255, cv2.THRESH_BINARY)

    # Mencari contour di gambar biner
    contours1, hierarchy1 = cv2.findContours(binary1, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contours2, hierarchy2 = cv2.findContours(binary2, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    # Menggambar contour di atas gambar original
    cv2.drawContours(img1, contours1, -1, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.drawContours(img2, contours2, -1, (0, 255, 0), 1, cv2.LINE_AA)

    # Mengganti ukuran gambar agar mempunyai resolusi yg sama
    img1 = cv2.resize(img1, (500, 300))
    img2 = cv2.resize(img2, (500, 300))

    # display both images
    cv2.imshow("One", img1)
    cv2.imshow("Two", img2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    similaritycheck = "{:.2f}".format(ssim(img1, img2) * 100)

    return float(similaritycheck)


def browsefunc(ent):
    filename = askopenfilename(filetypes=([
        ("image", ".jpeg"),
        ("image", ".png"),
        ("image", ".jpg"),
    ]))
    ent.delete(0, tk.END)
    ent.insert(tk.END, filename)


def checkSimilarity(window, path1, path2):
    result = match(path1=path1, path2=path2)
    if (result <= T):
        messagebox.showerror("Signatures Do Not Match",
                             "Signatures are " + str(result) + f" % similar!!")
        pass
    else:
        messagebox.showinfo("Signatures Match",
                            "Signatures are " + str(result) + f" % similar!!")
    return True


root = tk.Tk()
root.title("Signature Matching")
root.geometry("500x400")  # 300x200
uname_label = tk.Label(root, text="Signature Verification", font=10)
uname_label.place(x=160, y=50)

img1_message = tk.Label(root, text="Signature 1", font=10)
img1_message.place(x=10, y=120)

image1_path_entry = tk.Entry(root, font=10)
image1_path_entry.place(x=150, y=120)

img1_browse_button = tk.Button(
    root, text="Browse", font=10, command=lambda: browsefunc(ent=image1_path_entry))
img1_browse_button.place(x=400, y=110)

image2_path_entry = tk.Entry(root, font=10)
image2_path_entry.place(x=150, y=200)

img2_message = tk.Label(root, text="Signature 2", font=10)
img2_message.place(x=10, y=200)

img2_browse_button = tk.Button(
    root, text="Browse", font=10, command=lambda: browsefunc(ent=image2_path_entry))
img2_browse_button.place(x=400, y=190)

compare_button = tk.Button(
    root, text="Compare", font=10, command=lambda: checkSimilarity(window=root,
                                                                   path1=image1_path_entry.get(),
                                                                   path2=image2_path_entry.get(), ))

compare_button.place(x=200, y=300)
root.mainloop()

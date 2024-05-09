import matplotlib.pyplot as plt

# Örnek veri
x = [1, 2, 3, 4, 5]
y = [10, 20, 15, 25, 30]

# Bar plot çizimi
plt.bar(x, y)

# Y ekseninin maksimum değerini artırarak boşluk yaratma
max_y = max(y)
plt.ylim(0, max_y + max_y * 0.3) 

# Grafik gösterimi
plt.show()

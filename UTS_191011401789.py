# Nama   : Sendy Ramadhan Pratama
# NIM    : 191011401789
# Kelas  : 06TPLE025 

# Fuzzy Sugeno
# Studi Kasus : Restoran


def down(x, xmin, xmax):
    return (xmax- x) / (xmax - xmin)

def up(x, xmin, xmax):
    return (x - xmin) / (xmax - xmin)

# Banyak Pelanggan (minimal 40 orang dan maksimal 80 orang)
class Pelanggan():
    minimum = 145
    maximum = 240

    def sedikit(self, x):
        if x >= self.maximum:
            return 0
        elif x <= self.minimum:
            return 1
        else:
            return down(x, self.minimum, self.maximum)

    def banyak(self, x):
        if x >= self.maximum:
            return 1
        elif x <= self.minimum:
            return 0
        else:
            return up(x, self.minimum, self.maximum)


# Banyak Makanan (minimal 5, medium 10, dan maksimal 15)
class Makanan():
    minimum = 5
    medium = 15
    maximum = 25

    def sedikit(self, x):
        if x >= self.medium:
            return 0
        elif x <= self.minimum:
            return 1
        else:
            return down(x, self.minimum, self.medium)
    
    def cukup(self, x):
        if self.minimum < x < self.medium:
            return up(x, self.minimum, self.medium)
        elif self.medium < x < self.maximum:
            return down(x, self.medium, self.maximum)
        elif x == self.medium:
            return 1
        else:
            return 0

    def banyak(self, x):
        if x >= self.maximum:
            return 1
        elif x <= self.medium:
            return 0
        else:
            return up(x, self.medium, self.maximum)

# Kecepatan memasak (minimal 500 detik dan maksimal 2500 detik)
class Masak():
    minimum = 500
    maximum = 2500
    
    def kurang(self, α):
        return self.maximum - α * (self.maximum-self.minimum)

    def tambah(self, α):
        return α *(self.maximum - self.minimum) + self.minimum

    # 2 pelanggan 3 makanan
    def inferensi(self, jumlah_pelanggan, jumlah_makanan):
        plg = Pelanggan()
        mkn = Makanan()
        result = []

        # [R1] JIKA pelanggan SEDIKIT, dan makanan BANYAK, 
        #     MAKA kecepatan masak BERKURANG.
        α1 = min(plg.sedikit(jumlah_pelanggan), mkn.banyak(jumlah_makanan))
        z1 = self.kurang(α1)
        result.append((α1, z1))

        # [R2] JIKA pelanggan SEDIKIT, dan makanan SEDIKIT, 
        #     MAKA kecepatan masak BERKURANG.
        α2 = min(plg.sedikit(jumlah_pelanggan), mkn.sedikit(jumlah_makanan))
        z2 = self.kurang(α2)
        result.append((α2, z2))

        # [R3] JIKA pelanggan NAIK, dan makanan BANYAK, 
        #     MAKA kecepatan masak BERTAMBAH.
        α3 = min(plg.banyak(jumlah_pelanggan), mkn.banyak(jumlah_makanan))
        z3 = self.tambah(α3)
        result.append((α3, z3))
        
        # [R4] JIKA pelanggan NAIK, dan makanan SEDIKIT,
        #     MAKA kecepatan masak BERTAMBAH.
        α4 = min(plg.banyak(jumlah_pelanggan), mkn.sedikit(jumlah_makanan))
        z4 = self.tambah(α4)
        result.append((α4, z4))

        # [R5] JIKA pelanggan NAIK, dan makanan CUKUP,
        #     MAKA kecepatan masak BERKURANG.
        α5 = min(plg.banyak(jumlah_pelanggan), mkn.cukup(jumlah_makanan))
        z5 = self.kurang(α5)
        result.append((α5, z5))

        # [R6] JIKA pelanggan SEDIKIT, dan makanan CUKUP,
        #     MAKA kecepatan masak BERKURANG.
        α6 = min(plg.sedikit(jumlah_pelanggan), mkn.cukup(jumlah_makanan))
        z6 = self.tambah(α6)
        result.append((α6, z6))

        return result
    
    def defuzifikasi(self, jumlah_pelanggan, jumlah_makanan):
        inferensi_values = self.inferensi(jumlah_pelanggan, jumlah_makanan)
        return sum([(value[0]* value[1]) for value in inferensi_values]) / sum([value[0] for value in inferensi_values])
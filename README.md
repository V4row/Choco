# Choco
Belajar bersama Chef Chocowo

# Website Belajar Bareng

##Arti
- branch = cabang
- repo = gudang
- 
## Alur kerja 
1. Selalu `git pull` sebelum mulai kerja.
2. Buat perubahan di file masing-masing.
3. Simpan perubahan: `git add .`
4. Commit dengan pesan jelas: `git commit -m "A yang kau ubah"`
5. Push ke GitHub: `git push origin main` / `git push`

## Tips
- Jangan lupa `git pull` sebelum `git push`.
- Commit sering, jangan tunggu terlalu banyak perubahan.

##Fungsi Git
| Perintah Git                    | Fungsi Utama                                      | Kapan Dipakai            |
| ------------------------------- | ------------------------------------------------- | ------------------------ |
| `git pull origin main`          | Mengambil update terbaru dari GitHub              | Sebelum mulai kerja      |
| `git add .`                     | Menandai semua file yang diubah untuk commit      | Setelah edit file        |
| `git commit -m "pesan"`         | Menyimpan perubahan ke repo lokal dengan pesan    | Setelah `git add`        |
| `git push origin main`          | Mengirim commit lokal ke GitHub                   | Setelah commit           |
| `git status`                    | Mengecek status repo (file apa saja yang berubah) | Kapan saja               |
| `git log`                       | Melihat riwayat commit                            | Untuk mengecek histori   |
| `git checkout -b <nama-branch>` | Membuat branch baru & pindah ke branch itu        | Kalau kerja fitur khusus |
| `git merge <branch>`            | Menggabungkan branch ke branch aktif              | Setelah fitur selesai    |

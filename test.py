import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm

# Danh sách điểm số từ 40 bản ghi
scores = [5.5, 7.0, 6.0, 2.0, 5.0, 6.0, 9.0, 1.0, 5.5, 4.5, 
          8.0, 5.0, 6.0, 1.5, 5.0, 6.5, 9.5, 2.5, 5.5, 4.5, 
          7.5, 5.0, 6.0, 0.5, 4.5, 6.0, 10.0, 2.0, 5.5, 4.5, 
          8.0, 5.0, 6.0, 1.0, 4.5, 6.5, 9.0, 2.5, 5.5, 4.5]

# Tạo histogram
plt.figure(figsize=(10, 6))
n, bins, patches = plt.hist(scores, bins=np.arange(-0.25, 10.75, 0.5), 
                            color='skyblue', edgecolor='black', alpha=0.7, 
                            label='Điểm số')

# Vẽ đường cong phân phối chuẩn
x = np.linspace(0, 10, 100)
mean = np.mean(scores)
std = np.std(scores, ddof=1)
plt.plot(x, norm.pdf(x, mean, std) * n.sum() * 0.5, 'r-', lw=2, label='Phân phối chuẩn')

# Đặt tiêu đề và nhãn
plt.title('Phân phối điểm số (Trung bình: {:.1f}, Độ lệch chuẩn: {:.2f})'.format(mean, std), 
          fontsize=14, pad=10)
plt.xlabel('Điểm số (0-10)', fontsize=12)
plt.ylabel('Tần suất', fontsize=12)
plt.xticks(np.arange(0, 11, 1))
plt.grid(True, alpha=0.3)
plt.legend(fontsize=10)

# Cải thiện bố cục
plt.tight_layout()

# Hiển thị biểu đồ
plt.show()
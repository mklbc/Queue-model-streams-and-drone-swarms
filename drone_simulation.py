import numpy as np
from matplotlib import pyplot as plt


n = 5  
max_efficiency = 20 
queue_max_size = 20 
R = 100 
iterations = 100 
max_lifetime = 5 

s = np.array([10, 15, 20, 12, 8]) 
queues = np.zeros(n)  # Başlangıçta tüm kuyruklar boş
packet_lifetimes = [[] for _ in range(n)]  # Paketlerin yaşlarını takip eden listeler

# Paket dağıtımı ve kuyruk yönetimi fonksiyonu
def distribute_tasks_with_queues(s, R, queues, packet_lifetimes, max_lifetime):
    n = len(s)
    p = np.zeros(n)
    remaining_R = R

    # Kuyruklarda paket varsa, önce bunlar işlenir
    for i in range(n):
        if queues[i] > 0:
            to_process = min(queues[i], s[i])
            p[i] += to_process
            queues[i] -= to_process
            remaining_R -= to_process

    # Kalan paketler, uygun drone'lara dağıtılır
    while remaining_R > 0:
        for i in range(n):
            if remaining_R == 0:
                break
            if queues[i] < queue_max_size:
                queues[i] += 1
                remaining_R -= 1

    # Paket yaşlarını güncelle ve eski paketleri çıkar
    for i in range(n):
        packet_lifetimes[i] = [age + 1 for age in packet_lifetimes[i]] + [0] * int(queues[i] - len(packet_lifetimes[i]))
        packet_lifetimes[i] = [age for age in packet_lifetimes[i] if age <= max_lifetime]
        queues[i] = len(packet_lifetimes[i])

    return p, queues, packet_lifetimes

# Simülasyonu gerçekleştir
queue_sizes_over_time = np.zeros((iterations, n))
for t in range(iterations):
    _, queues, packet_lifetimes = distribute_tasks_with_queues(s, R, queues, packet_lifetimes, max_lifetime)
    queue_sizes_over_time[t] = queues

# Sonuçları görselleştir
plt.figure(figsize=(10, 6))
for i in range(n):
    plt.plot(range(iterations), queue_sizes_over_time[:, i], label=f'Drone {i + 1}')
plt.xlabel('Iteration')
plt.ylabel('Queue Size')
plt.title('Drone Queue Sizes Over Time')
plt.legend()
plt.show()

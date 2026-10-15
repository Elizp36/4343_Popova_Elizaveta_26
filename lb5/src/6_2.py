from collections import deque

class Node:
    def __init__(self):
        self.children = {} #Вершины-дети
        self.suffix_link = None
        self.output_link = None
        self.segment_ids = []  #Храним ID сегментов, которые заканчиваются в этой вершине
        self.depth = 0

class AhoCorasick:
    #Создаём корень
    def __init__(self):
        self.root = Node()
        self.root.suffix_link = self.root
        self.root.output_link = None
        self.segments = []  #список номера терминальных вершин
    
    def add_segment(self, segment, segment_id):
        node = self.root
        for char in segment: #a в сегменте
            if char not in node.children: #Если не в боре
                new_node = Node()   #Создаём вершину
                new_node.depth = node.depth + 1
                node.children[char] = new_node
            node = node.children[char]
        node.segment_ids.append(segment_id) #Сегмент закончился добавляем в массив его номер 0

    #Построение ссылок
    def build_automaton(self):
        queue = deque()
        for char, child in self.root.children.items():
            child.suffix_link = self.root
            child.output_link = None
            queue.append(child)
        
        #BFS для построения ссылок
        while queue:
            current = queue.popleft()
            for char, child in current.children.items():
                #Ищем суффиксную ссылку
                suffix_node = current.suffix_link
                while suffix_node != self.root and char not in suffix_node.children:
                    suffix_node = suffix_node.suffix_link
                
                if char in suffix_node.children:
                    child.suffix_link = suffix_node.children[char]
                else:
                    child.suffix_link = self.root
                
                #Строим сжатую суффиксную ссылку
                if child.suffix_link.segment_ids:
                    child.output_link = child.suffix_link
                else:
                    child.output_link = child.suffix_link.output_link
                
                queue.append(child)
    
    def search_and_count(self, text, m, segments_info):
        #text - исходный текст
        #m - длина полного шаблона с джокерами
        #segments_info - список кортежей (отступ, длина сегмента)
        n = len(text)
        C = [0] * (n + 1) #массив для опрределения вхождения
        
        node = self.root
        for i, char in enumerate(text):
            #Относится к ленивой реализации (здесь мы ходим по суффиксным ссылкам)
            while node != self.root and char not in node.children:
                node = node.suffix_link
            
            if char in node.children:
                node = node.children[char]
            else:
                node = self.root
            
            temp = node
            while temp is not None and temp != self.root:
                for seg_id in temp.segment_ids:
                    offset, seg_len = segments_info[seg_id]
                    
                    start_pos = i - seg_len + 1 #Позиция начала этого сегмента в тексте (считаем с 0)
                    
                    #Вычисляем, с какой позиции должен начинаться весь шаблон
                    template_start = start_pos - offset
                    
                    #Проверяем, что эта стартовая позиция не выходит за границы
                    if template_start >= 0 and template_start + m <= n:
                        #голосуем за эту позицию, как гачала шаблона.
                        #Чем больше голосов, тем больше вероятность, что мы начали именно там
                        C[template_start] += 1 
                        
                
                temp = temp.output_link
        
        #Ответ там, где счётчик равен общему числу сегментов
        num_segments = len(segments_info)
        results = []
        for i in range(n - m + 1):
            if C[i] == num_segments:
                results.append(i + 1)  # Переводим в нумерацию от 1 для вывода
                
        return results

def solve():
    text = input().strip()
    pattern = input().strip()
    wildcard = input().strip()
    
    n = len(text)
    m = len(pattern)

    segments_info = []  #Будет хранить информацию о сегментах: [(0, ab),(4, c)]
    current_segment = [] #подстрока без джокеров
    current_offset = 0 #отступ от начала
    
    for i, char in enumerate(pattern):
        if char == wildcard:
            if current_segment:
                seg_str = "".join(current_segment) #формирование строки
                segments_info.append((current_offset, seg_str)) #Сохранение иинформации (отступа и самой строки)
                current_segment = [] #очищение
            current_offset = i + 1 #увеличение отступа
        else:
            if not current_segment:
                current_offset = i
            current_segment.append(char)
    #Если паттерн будет заканчиваться на букве, то мы тут досохраняем информацию        
    if current_segment:
        segments_info.append((current_offset, "".join(current_segment)))
    
    if not segments_info:
        for i in range(1, n - m + 2):
            print(i)
        return
    
    #Построение автомата Ахо-Корасик для сегментов
    ac = AhoCorasick()
    for seg_id, (_, seg_str) in enumerate(segments_info):
        ac.segments.append(seg_str)
        ac.add_segment(seg_str, seg_id)
    ac.build_automaton()
    
    #новый список, хранящий отступ и длину каждого сегмента
    seg_checks = [(offset, len(seg_str)) for offset, seg_str in segments_info]
    
    results = ac.search_and_count(text, m, seg_checks)
    
    for pos in results:
        print(pos)

if __name__ == "__main__":
    solve()
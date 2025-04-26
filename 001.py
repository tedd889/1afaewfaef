import tkinter as tk
from tkinter import messagebox
import random
import heapq


class MazeGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("迷宫生成器 - 最优路径版")

        # 迷宫参数
        self.width = 20
        self.height = 20
        self.cell_size = 20
        self.maze = None
        self.solution_path = []

        # 创建UI
        self.create_widgets()

    def create_widgets(self):
        # 控制面板
        control_frame = tk.Frame(self.root)
        control_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        # 尺寸设置
        size_frame = tk.LabelFrame(control_frame, text="迷宫尺寸")
        size_frame.pack(pady=5)

        tk.Label(size_frame, text="宽度(X):").grid(row=0, column=0)
        self.width_entry = tk.Entry(size_frame)
        self.width_entry.grid(row=0, column=1)
        self.width_entry.insert(0, "20")

        tk.Label(size_frame, text="高度(Y):").grid(row=1, column=0)
        self.height_entry = tk.Entry(size_frame)
        self.height_entry.grid(row=1, column=1)
        self.height_entry.insert(0, "20")

        # 功能按钮
        button_frame = tk.Frame(control_frame)
        button_frame.pack(pady=10)

        self.generate_btn = tk.Button(button_frame, text="生成迷宫", command=self.generate_maze)
        self.generate_btn.pack(fill=tk.X, pady=5)

        self.show_path_btn = tk.Button(button_frame, text="显示最优路径", command=self.show_optimal_path,
                                       state=tk.DISABLED)
        self.show_path_btn.pack(fill=tk.X, pady=5)

        self.reset_btn = tk.Button(button_frame, text="重新开始", command=self.reset)
        self.reset_btn.pack(fill=tk.X, pady=5)

        # 迷宫画布
        self.canvas = tk.Canvas(self.root, width=self.width * self.cell_size, height=self.height * self.cell_size,
                                bg="white")
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)

    def generate_maze(self):
        try:
            self.width = int(self.width_entry.get())
            self.height = int(self.height_entry.get())
            if self.width < 5 or self.height < 5:
                raise ValueError("尺寸太小")
            if self.width > 50 or self.height > 50:
                raise ValueError("尺寸太大")
        except ValueError as e:
            messagebox.showerror("错误", f"请输入5-50之间的整数\n{str(e)}")
            return

        # 重置画布
        self.canvas.config(width=self.width * self.cell_size, height=self.height * self.cell_size)
        self.canvas.delete("all")

        # 初始化迷宫 (0=墙, 1=路)
        self.maze = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.solution_path = []

        # 使用深度优先算法生成迷宫
        self.dfs_maze_generation()

        # 绘制迷宫
        self.draw_maze()

        # 启用显示路径按钮
        self.show_path_btn.config(state=tk.NORMAL)

    def dfs_maze_generation(self):
        # 设置入口(0,1)和出口(height-1, width-2)
        start_x, start_y = 1, 0
        end_x, end_y = self.width - 2, self.height - 1

        # 标记入口和出口
        self.maze[start_y][start_x] = 1
        self.maze[end_y][end_x] = 1

        # 从起点开始生成路径
        stack = [(start_x, start_y)]
        visited = set()
        visited.add((start_x, start_y))

        # 四个可能的方向
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        while stack:
            x, y = stack[-1]
            neighbors = []

            # 检查四个方向的邻居
            for dx, dy in directions:
                nx, ny = x + dx * 2, y + dy * 2  # 每次移动两步，确保有墙
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if (nx, ny) not in visited:
                        neighbors.append((dx, dy, nx, ny))

            if neighbors:
                # 随机选择一个方向
                dx, dy, nx, ny = random.choice(neighbors)
                # 打通墙壁
                self.maze[y + dy][x + dx] = 1
                self.maze[ny][nx] = 1
                visited.add((nx, ny))
                stack.append((nx, ny))
            else:
                stack.pop()

        # 确保出口被连接
        if (end_x, end_y) not in visited:
            # 找到最近的已访问点连接到出口
            for dx, dy in directions:
                nx, ny = end_x + dx, end_y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if self.maze[ny][nx] == 1:
                        self.maze[end_y][end_x] = 1
                        self.maze[ny][nx] = 1
                        break

    def find_optimal_path(self):
        if not self.maze:
            return []

        # 定义起点和终点
        start = (1, 0)  # 入口
        end = (self.width - 2, self.height - 1)  # 出口

        # 四个可能的方向
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        # Dijkstra算法寻找最短路径
        heap = []
        heapq.heappush(heap, (0, start, [start]))
        visited = set()
        visited.add(start)

        while heap:
            cost, (x, y), path = heapq.heappop(heap)

            if (x, y) == end:
                return path

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if self.maze[ny][nx] == 1 and (nx, ny) not in visited:
                        visited.add((nx, ny))
                        heapq.heappush(heap, (cost + 1, (nx, ny), path + [(nx, ny)]))

        return []  # 没有找到路径

    def draw_maze(self):
        self.canvas.delete("all")

        # 绘制墙壁
        for y in range(self.height):
            for x in range(self.width):
                if self.maze[y][x] == 0:  # 墙
                    self.canvas.create_rectangle(
                        x * self.cell_size, y * self.cell_size,
                        (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                        fill="black", outline="black"
                    )

        # 标记入口和出口
        self.canvas.create_rectangle(
            1 * self.cell_size, 0 * self.cell_size,
            2 * self.cell_size, 1 * self.cell_size,
            fill="green", outline="green"
        )
        self.canvas.create_rectangle(
            (self.width - 2) * self.cell_size, (self.height - 1) * self.cell_size,
            (self.width - 1) * self.cell_size, self.height * self.cell_size,
            fill="red", outline="red"
        )

    def show_optimal_path(self):
        # 找到最优路径
        self.solution_path = self.find_optimal_path()

        if not self.solution_path:
            messagebox.showinfo("提示", "没有找到路径！")
            return

        # 绘制路径
        for i in range(len(self.solution_path) - 1):
            x1, y1 = self.solution_path[i]
            x2, y2 = self.solution_path[i + 1]

            # 绘制路径线
            self.canvas.create_line(
                (x1 + 0.5) * self.cell_size, (y1 + 0.5) * self.cell_size,
                (x2 + 0.5) * self.cell_size, (y2 + 0.5) * self.cell_size,
                fill="blue", width=2
            )

        # 标记起点和终点
        self.canvas.create_oval(
            1.25 * self.cell_size, 0.25 * self.cell_size,
            1.75 * self.cell_size, 0.75 * self.cell_size,
            fill="yellow", outline="yellow"
        )
        self.canvas.create_oval(
            (self.width - 1.75) * self.cell_size, (self.height - 0.75) * self.cell_size,
            (self.width - 1.25) * self.cell_size, (self.height - 0.25) * self.cell_size,
            fill="yellow", outline="yellow"
        )

    def reset(self):
        self.canvas.delete("all")
        self.maze = None
        self.solution_path = []
        self.show_path_btn.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = MazeGenerator(root)
    root.mainloop()
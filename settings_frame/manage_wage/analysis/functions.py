def update_Graph(figure, line, ax, dic, kind="line"):
    # dic = {"name" : [df, 1]}
    ax.clear() # 수행 전, 그려진 그래프 지움. 안하면 기존 그래프에 덧그림
    for value in dic.values():
        if value[1]:
            value[0].plot(kind=kind, legend=True, ax=ax, marker='o', fontsize=10)
    figure.canvas.draw()
    figure.canvas.flush_events()
    return

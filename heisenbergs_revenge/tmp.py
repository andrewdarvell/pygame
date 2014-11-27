# coding utf-8

def loadLevel(name):
    global playerX, playerY # объявляем глобальные переменные, это координаты героя
    global total_level_height, total_level_width
    global sprite_layers # все слои карты

    world_map = tmxreader.TileMapParser().parse_decode('%s/%s.tmx' % (FILE_DIR, name)) # загружаем карту
    resources = helperspygame.ResourceLoaderPygame() # инициируем преобразователь карты
    resources.load(world_map) # и преобразуем карту в понятный pygame формат

    sprite_layers = helperspygame.get_layers_from_map(resources) # получаем все слои карты

    # берем слои по порядку 0 - слой фона, 1- слой блоков, 2 - слой смертельных блоков
    # 3 - слой объектов монстров, 4 - слой объектов телепортов
    platforms_layer = sprite_layers[1]
    dieBlocks_layer = sprite_layers[2]

    for row in range(0, platforms_layer.num_tiles_x): # перебираем все координаты тайлов
        for col in range(0, platforms_layer.num_tiles_y):
            if platforms_layer.content2D[col][row] is not None:
                pf = Platform(row * PLATFORM_WIDTH, col * PLATFORM_WIDTH)# как и прежде создаем объкты класса Platform
                platforms.append(pf)
            if dieBlocks_layer.content2D[col][row] is not None:
                bd = BlockDie(row * PLATFORM_WIDTH, col * PLATFORM_WIDTH)
                platforms.append(bd)

    teleports_layer = sprite_layers[4]
    for teleport in teleports_layer.objects:
        try: # если произойдет ошибка на слое телепортов
            goX = int(teleport.properties["goX"]) * PLATFORM_WIDTH
            goY = int (teleport.properties["goY"]) * PLATFORM_HEIGHT
            x = teleport.x
            y = teleport.y - PLATFORM_HEIGHT
            tp = BlockTeleport(x, y, goX, goY)
            entities.add(tp)
            platforms.append(tp)
            animatedEntities.add(tp)
        except: # то игра не вылетает, а просто выводит сообщение о неудаче
            print(u"Ошибка на слое телепортов")

    monsters_layer = sprite_layers[3]
    for monster in monsters_layer.objects:
        try:
            x = monster.x
            y = monster.y
            if monster.name == "Player":
                playerX = x
                playerY = y - PLATFORM_HEIGHT
            elif monster.name == "Princess":
                pr = Princess(x, y - PLATFORM_HEIGHT)
                platforms.append(pr)
                entities.add(pr)
                animatedEntities.add(pr)
            else:
                up = int(monster.properties["up"])
                maxUp = int(monster.properties["maxUp"])
                left = int(monster.properties["left"])
                maxLeft = int(monster.properties["maxLeft"])
                mn = Monster(x, y - PLATFORM_HEIGHT, left, up, maxLeft, maxUp)
                entities.add(mn)
                platforms.append(mn)
                monsters.add(mn)
        except:
            print(u"Ошибка на слое монстров")

    total_level_width = platforms_layer.num_tiles_x * PLATFORM_WIDTH # Высчитываем фактическую ширину уровня
    total_level_height = platforms_layer.num_tiles_y * PLATFOR
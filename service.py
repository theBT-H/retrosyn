import os
import traceback

from learn_flask.exts import db


class BiNode(object):
    def __init__(self, element=None, left=None, right=None):
        self.element = element
        self.left = left
        self.right = right

    def get_element(self):
        return self.element

    def dict_form(self):
        dict_set = {
            "element": self.element,
            "left": self.left,
            "right": self.right,
        }
        return dict_set

    def __str__(self):
        return str(self.element)


import matplotlib.pyplot as plt


class BiTree:
    def __init__(self, tree_node=None):
        self.root = tree_node

    def set_up_from_dict(self, dict_instance):
        if not isinstance(dict_instance, dict):
            return None
        else:
            dict_queue = list()
            node_queue = list()
            node = BiNode(dict_instance["element"])
            self.root = node
            node_queue.append(node)
            dict_queue.append(dict_instance)
            while len(dict_queue):
                dict_in = dict_queue.pop(0)
                node = node_queue.pop(0)
                if isinstance(dict_in.get("left", None), (dict, int, float, str)):
                    if isinstance(dict_in.get("left", None), dict):
                        dict_queue.append(dict_in.get("left", None))
                        left_node = BiNode(dict_in.get("left", None)["element"])
                        node_queue.append(left_node)
                    else:
                        left_node = BiNode(dict_in.get("left", None))
                    node.left = left_node

                if isinstance(dict_in.get("right", None), (dict, int, float, str)):
                    if isinstance(dict_in.get("right", None), dict):
                        dict_queue.append(dict_in.get("right", None))
                        right_node = BiNode(dict_in.get("right", None)["element"])
                        node_queue.append(right_node)
                    else:
                        right_node = BiNode(dict_in.get("right", None))
                    node.right = right_node

    def pack_to_dict(self):
        if self.root is None:
            return None
        else:
            node_queue = list()
            dict_queue = list()
            node_queue.append(self.root)
            dict_pack = self.root.dict_form()
            dict_queue.append(dict_pack)
            while len(node_queue):
                q_node = node_queue.pop(0)
                dict_get = dict_queue.pop(0)
                if q_node.left is not None:
                    node_queue.append(q_node.left)
                    dict_get["left"] = q_node.left.dict_form()
                    dict_queue.append(dict_get["left"])
                if q_node.right is not None:
                    node_queue.append(q_node.right)
                    dict_get["right"] = q_node.right.dict_form()
                    dict_queue.append(dict_get["right"])
        return dict_pack

    def get_depth(self):
        if self.root is None:
            return 0
        else:
            node_queue = list()
            node_queue.append(self.root)
            depth = 0
            while len(node_queue):
                q_len = len(node_queue)
                while q_len:
                    q_node = node_queue.pop(0)
                    q_len = q_len - 1
                    if q_node.left is not None:
                        node_queue.append(q_node.left)
                    if q_node.right is not None:
                        node_queue.append(q_node.right)
                depth = depth + 1
            return depth

    def view_in_graph(self, image_path):
        if self.root is None:
            print("An Empty Tree, Nothing to plot")
        else:
            temp = []
            depth = self.get_depth()

            node_plot = NodePlot()

            ax = node_plot.draw_init()
            coord0 = (1 / (2 * depth), 1 / 2)
            temp.append(coord0)
            node_queue = list()
            coord_queue = list()
            node_plot.plot_node(ax, str(self.root.get_element()), coord0, coord0)
            node_queue.append(self.root)
            coord_queue.append(coord0)
            cur_level = 0
            while len(node_queue):
                q_len = len(node_queue)
                while q_len:
                    q_node = node_queue.pop(0)
                    coord_prt = coord_queue.pop(0)
                    q_len = q_len - 1
                    if q_node.left is not None:
                        xc, yc = node_plot.get_coord(coord_prt, cur_level + 1, depth, "left")
                        temp.append((xc, yc))
                        element = str(q_node.left.get_element())
                        node_plot.plot_node(ax, element, (xc, yc), coord_prt)
                        node_queue.append(q_node.left)
                        coord_queue.append((xc, yc))
                    if q_node.right is not None:
                        xc, yc = node_plot.get_coord(coord_prt, cur_level + 1, depth, "right")
                        temp.append((xc, yc))
                        element = str(q_node.right.get_element())
                        node_plot.plot_node(ax, element, (xc, yc), coord_prt)
                        node_queue.append(q_node.right)
                        coord_queue.append((xc, yc))
                cur_level += 1
            node_plot.savefig(image_path)
            return temp

class NodePlot():

    def __init__(self, label='BinaryTree'):
        self.label = label
    def draw_init(self):
        fig = plt.figure(self.label, figsize=(70,60))
        ax = fig.add_subplot(111)
        return ax
    def get_coord(self, coord_prt, depth_le, depth, child_type="left"):
        if child_type == "left":
            y_child = coord_prt[1] - 1 / (2 ** (depth_le + 1))
        elif child_type == "right":
            y_child = coord_prt[1] + 1 / (2 ** (depth_le + 1))
        else:
            raise Exception("illegal child type")
        x_child = coord_prt[0] + 1 / depth
        return x_child, y_child
    def plot_node(self, ax, node_text, center_point, parent_point):
        ax.annotate(node_text, xy=parent_point, xycoords='axes fraction', xytext=center_point, textcoords='axes fraction', va="bottom", ha="right", size=46, bbox= dict(boxstyle="round", fc='lightcyan', lw=2), arrowprops=dict(arrowstyle="<-", facecolor='black', lw=2))
    def show(self):
        plt.show()
    def savefig(self, fileName):
        plt.savefig(fileName, dpi=72, bbox_inches='tight', pad_inches = -0.1)

from PIL import Image

def Picture_Synthesis(mother_img,
                      son_img,
                      save_img,
                      coordinate=None):
    """
    :param mother_img: 母图
    :param son_img: 子图
    :param save_img: 保存图片名
    :param coordinate: 子图在母图的坐标
    :return:
    """
    #将图片赋值,方便后面的代码调用
    M_Img = Image.open(mother_img)
    S_Img = Image.open(son_img)
    factor = 1#子图缩小的倍数1代表不变，2就代表原来的一半

    #给图片指定色彩显示格式
    M_Img = M_Img.convert("RGBA")  # CMYK/RGBA 转换颜色格式（CMYK用于打印机的色彩，RGBA用于显示器的色彩）

    # 获取图片的尺寸
    M_Img_w, M_Img_h = M_Img.size  # 获取被放图片的大小（母图）
    #print("母图尺寸：",M_Img.size)
    S_Img_w, S_Img_h = S_Img.size  # 获取小图的大小（子图）
    #print("子图尺寸：",S_Img.size)

    size_w = int(S_Img_w / factor)
    size_h = int(S_Img_h / factor)

    # 防止子图尺寸大于母图
    if S_Img_w > size_w:
        S_Img_w = size_w
    if S_Img_h > size_h:
        S_Img_h = size_h

    # # 重新设置子图的尺寸
    # icon = S_Img.resize((S_Img_w, S_Img_h), Image.ANTIALIAS)
    icon = S_Img.resize((S_Img_w, S_Img_h), Image.ANTIALIAS)
    w = int((M_Img_w - S_Img_w) / 2)
    h = int((M_Img_h - S_Img_h) / 2)
    #print(w)
    #print(h)

    try:
        if coordinate==None or coordinate=="":
            coordinate=(w, h)
            # 粘贴子图到母图的指定坐标（当前居中）
            M_Img.paste(icon, coordinate, mask=None)
        else:
            #print("已经指定坐标")
            # 粘贴子图到母图的指定坐标（当前居中）
            M_Img.paste(icon, coordinate, mask=None)
    except:
        pass
        #print("坐标指定出错 ")
    # 保存图片
    M_Img.save(save_img)


from rdkit import Chem
from rdkit.Chem import Draw, MolFromSmiles
from rdkit.Chem import BRICS
from rdkit.Chem import rdDepictor


def getMax2Structure(now):
    for i in range(100):
        res = list(BRICS.BRICSDecompose(now, minFragmentSize=i))
        if len(res) == 2:
            return i
    return -1


def getMaxNum(m):
    mol = Chem.MolFromSmiles(m)
    res = list(BRICS.BRICSDecompose(mol))
    length = 0
    while 2 ** length <= len(res):
        length += 1
    return 2 ** length


def getAdlist(m, smis):#函数返回列表mat，该列表包含了化合物的BRICS分解树的拓扑结构的二进制编码。1表示当前节点为非叶节点，0表示当前节点为叶节点。
    length = getMaxNum(m)
    num = length * 2 - 1
    mat = [1] * num
    i = 0
    j = 0
    while i < num and j < len(smis):
        if mat[i] == 1 and smis[j] is not None:
            i += 1
            j += 1
        elif mat[i] == 1 and smis[j] is None:
            cur = i - 1
            cur = []
            cur.append(i - 1)
            while cur:
                pop_num = cur[0]
                cur.pop(0)
                left = pop_num * 2 + 1
                right = left + 1
                if left > num - 1:
                    break
                else:
                    cur.append(left)
                    cur.append(right)
                    mat[left] = 0
                    mat[right] = 0
            j += 1
        elif mat[i] == 0:
            i += 1
    return mat


def getAllStructure(m,option):
    smis = []
    q = []
    rdk = []
    mol = Chem.MolFromSmiles(m)
    q.append(mol)
    rdk.append(m)
    while q:
        now = rdk[0]
        cur = q[0]
        q.pop(0)
        rdk.pop(0)
        smis.append(now)
        minsize = getMax2Structure(cur)
        if minsize == -1:
            smis.append(None)
            continue
        else:
            p = []

            if option == 1:
                res = newSingleSyn(cur, minsize)
            else:#选择调用数据库
                try:
                    with db.cursor() as cursor:
                        sql = "SELECT product FROM singlesyn WHERE product = %s"
                        product = Chem.MolToSmiles(cur)
                        cursor.execute(sql, (product,))
                        result = cursor.fetchone()
                        if not result:
                            res = newSingleSyn(cur, minsize)
                        else:
                            reactants = int(result[0][2])
                            res = tuple(reactants.split(','))
                except:
                    res = newSingleSyn(cur, minsize)
                finally:
                    cursor.close()

            for i in range(len(res)):
                change = Chem.MolFromSmiles(res[i])
                p.append(change)
            q += p
            rdk += res
    return smis

def newSingleSyn(cur,minsize):
    res = list(BRICS.BRICSDecompose(cur, minFragmentSize=minsize))  # 单步逆合成
    res.reverse()
    # 将单步逆合成结果存入数据库
    try:
        with db.cursor() as cursor:
            sql = "SELECT product FROM singlesyn WHERE product = %s"
            product = Chem.MolToSmiles(cur)
            cursor.execute(sql, (product,))
            result = cursor.fetchone()
            if not result:
                reactants = ','.join(res)
                sql = "INSERT INTO singlesyn(product, reactants) VALUES (%s, %s)"
                params = (product, reactants)
                try:
                    with db.cursor() as cursor1:
                        cursor1.execute(sql, params)
                        db.commit()
                except Exception as e:
                    traceback.print_exc()
                    db.rollback()
                finally:
                    cursor1.close()

    finally:
        cursor.close()
    return res


def transForm(mat, smis):
    length = len(mat)
    tlength = len(smis)
    mols = list()
    i = 0
    j = 0
    while i < length and j < tlength:
        if mat[i] == 1 and smis[j] is not None:
            mols.append(smis[j])
            i += 1
            j += 1
        elif mat[i] == 1 and smis[j] is None:
            j += 1
        elif mat[i] == 0:
            mols.append(None)
            i += 1
    return mols


def list_to_binarytree(mols):
    def level(index):
        if index >= len(mols) or mols[index] is None:
            return None

        root = BiNode(element=mols[index])
        root.left = level(2 * index + 1)
        root.right = level(2 * index + 2)
        return root

    return level(0)


def savePic(mols):
    length = len(mols)
    j = 0
    for i in range(length):
        if mols[i] is not None:
            mol = Chem.MolFromSmiles(mols[i])
            Draw.MolToFile(mol, 'D:/retrosynData/data/pic/temp{}.png'.format(j), size=(200, 200))
            j += 1

def resyn(m,id,option):
    smis = getAllStructure(m, option)
    mat = getAdlist(m, smis)
    res = transForm(mat, smis)
    tree = BiTree()
    root = list_to_binarytree(res)
    savePic(res)

    try:
        # 查询是否已存在该用户与产物的历史记录
        sql = "SELECT route_id FROM route WHERE user_id = %s AND product = %s"
        cursor = db.cursor()
        cursor.execute(sql, (id, m,))
        result = cursor.fetchone()
        if result:
            num = int(result[0])


    # except Exception as e:
    #     traceback.print_exc()
    #     flash("查询出错: {}".format(str(e)))
    finally:
        cursor.close()
    mol = MolFromSmiles(m)
    imgS = Draw.MolToImage(mol, size=(100, 100))
    imgS_name = 'mol_%d.png' % num
    imgS_path = 'D:/retrosynData/data/thumbnail/'+imgS_name
    imgS.save(imgS_path)
    folder_name = "D:/retrosynData/data/route"
    image_path= folder_name + '/result_%d.png' % num

    tree.root = root
    tree.root.element = 'target_molecule'
    temp = tree.view_in_graph(image_path)
    place = []
    for i in range(len(temp)):
        list1 = list(temp[i])
        list2 = [0, 0]
        list2[0] = int(3922 * list1[0])
        list2[1] = int(3268 - 3268 * list1[1])
        tup = tuple(list2)
        place.append(tup)
    # print(place)



    for i in range(len(temp)):
        Picture_Synthesis(mother_img=image_path,
                          son_img="D:/retrosynData/data/pic/temp{}.png".format(i),
                          save_img=image_path,
                          coordinate=place[i]
                          )

    try:
        with db.cursor() as cursor:
            # 插入
            sql = "UPDATE route SET route = %s, product_pic = %s WHERE user_id = %s AND product = %s"
            params = (image_path, imgS_name, id, m,)
            # 执行 SQL 语句
            cursor.execute(sql, params)
            db.commit()
    except:
        traceback.print_exc()
        db.rollback()
    finally:
        # 关闭数据库连接
        cursor.close()
    img = image_path

    return img

import os
path_need_to_rename = [r"../DataSet/images/", r"../DataSet/Annotations/"]
# Attention: You must add "/" at the end of the path.


def rename(path):
    filename_list = os.listdir(path)
    a = 100000
    for i in filename_list:
        used_name = path + i
        new_name = path + str(a).zfill(6) + f".{i.split('.')[-1]}" # 保留原后缀
        os.rename(used_name, new_name)
        print("File %s successfully renamed, new name is %s" %(used_name,new_name))
        a += 1

if __name__=='__main__':
    for path in path_need_to_rename:
        rename(path)

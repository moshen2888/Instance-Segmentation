
from utility.rle_tool import *
from utility.tool import *
import os
from config.config import *

column_name_img_id = 'id'
column_name_annotation = 'annotation'


class TrainLabelsProcessor(object):
    def __init__(self):

        self.dir_train_csv = TRAIN_CSV
        self.save_mask_dir = MASK_DIR

        self.dict_imgID_rel = {}  # key is image id, v is rel code but store by lines
        self.dict_imgID_mask = {}  # key is image id, v is mask

        data_exist_bool = os.path.exists(self.save_mask_dir)

        if not data_exist_bool:
            self.get_dict_imgID_mask()
        else:
            self.dict_imgID_rel = load_dict_from_csv(self.save_mask_dir)
            for img_id, rles in self.dict_imgID_rel.items():
                current_mask = rle_decode(rles, (HEIGHT, WIDTH))
                self.dict_imgID_mask[img_id] = current_mask

    def __len__(self):
        return len(self.dict_imgID_mask)

    def get_dict_imgID_mask(self):
        train_frame = pd.read_csv(self.dir_train_csv)
        # print(train_frame[column_name_annotation][0:5])
        self.dict_imgID_rel = {}  # key is image id, v is rel code but store by lines

        num_lenth = len(train_frame[column_name_img_id])

        for i in range(num_lenth):
            img_id = train_frame[column_name_img_id][i]
            rle_code = train_frame[column_name_annotation][i]
            if img_id in self.dict_imgID_rel:
                rles = self.dict_imgID_rel[img_id]
                rles = rles + ' ' + rle_code  # note we need a space here
                self.dict_imgID_rel[img_id] = rles
            else:
                self.dict_imgID_rel[img_id] = rle_code
        save_dict_as_csv(self.save_mask_dir, self.dict_imgID_rel)

import json

from mt_cv import image_util


def export_json(land_dict):
    json_data = json.dumps(land_dict, sort_keys=True, indent=4, separators=(',', ': '))
    # print(json_data)

    with open(image_util.img_abs_path('/images/tmp/json/data.json'), 'w') as f:
        json.dump(json_data, f)


def import_json():
    with open(image_util.img_abs_path('/images/tmp/json/data.json'), 'w') as f:
        json_data = json.load(f)

        # todo 如何将json_data转换成InputData
        input_data = json.loads(json_data)


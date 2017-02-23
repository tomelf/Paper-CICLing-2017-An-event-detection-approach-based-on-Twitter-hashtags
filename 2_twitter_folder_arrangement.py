# Step 2: tweet folder arrangement #

import os
import shutil

def main():
    min_cluster_hour = 24

    dest_folder = "preprocessed_must_contain_location"
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    src_folder = "must_contain_location"
    src_files = os.listdir(src_folder)
    for file_name in src_files:
        full_file_name = os.path.join(src_folder, file_name)
        if (os.path.isfile(full_file_name)):
            shutil.copy(full_file_name, dest_folder)

    filelist = os.listdir(dest_folder)

    for filepath in filelist:
        items = filepath.split('.')
        if items[0] == "export":
            date, hour = items[1].split('_')
            hour = int(hour)

            target_folder = os.path.join(
                dest_folder,
                "{0}_{1:d}".format(
                    date, 1 + hour/min_cluster_hour
                )
            )

            if not os.path.exists(target_folder):
                os.makedirs(target_folder)

            modified_filepath = "{0}.{1}".format("preprocessed", ".".join(items[1:]))
            os.rename(os.path.join(dest_folder, filepath), os.path.join(target_folder, modified_filepath))

if __name__ == '__main__':
    main()

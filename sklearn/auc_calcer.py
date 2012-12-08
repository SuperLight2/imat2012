def calc_auc(answers):
    class_plus = 0
    class_minus = 0
    for answer in answers:
        if answer == 1:
            class_plus += 1
        else:
            class_minus += 1

    tpr = 0
    auc = 0
    for answer in answers:
        if answer != 1:
            auc += 1.0 * tpr / class_minus
        else:
            tpr += 1.0 / class_plus
    return auc


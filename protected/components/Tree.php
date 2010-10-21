<?php

class Tree extends CWidget {
    public function run() {
        $model = Interests::model()->findByPK(1); // Здесь вместо Categories меняем на свою модель
        $tree = $model->getTreeViewData(false);
        $this->render('tree',array('tree'=>$tree,));
    }
}

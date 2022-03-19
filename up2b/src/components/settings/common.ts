import { ImageCodes } from '../../apis/consts'
import { Tag } from '../../apis/interfaces'

export const addTag = (tags: Tag[], imageCode: number) => {
    let exits = false, darkIdx = -1
    for (let i = 0; i < tags.length; i++) {
        const tag = tags[i] as Tag
        if (tag.index == imageCode) {
            exits = true
        } else {
            if (tag.effect == 'dark') {
                darkIdx = i
            }
        }
    }

    if (!exits && darkIdx >= 0) {
        (tags[darkIdx] as Tag).effect = 'plain';
        (tags as Tag[]).push({
            index: imageCode,
            name: ImageCodes[imageCode],
            effect: 'dark'
        })
    }
}

export const switchTag = (tags: Tag[], idx: number) => {
    console.log('切换到', idx)
    for (let i = 0; i < tags.length; i++) {
        if ((tags[i] as Tag).index == idx) {
            (tags[i] as Tag).effect = 'dark'
        } else {
            (tags[i] as Tag).effect = 'plain'
        }
    }
}
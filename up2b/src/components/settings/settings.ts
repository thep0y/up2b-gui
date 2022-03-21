import type { Tag, ImageListType } from '../../apis'
import { ImageCodes } from '../../apis'

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
    tags.forEach(v => {
        if (idx == v.index) {
            v.effect = 'dark'
        } else {
            if (v.effect === 'dark') {
                v.effect = 'plain'
            }
        }
    })
}

export const clearImageList = (imageList: ImageListType) => {
    imageList.splice(0, imageList.length)
}

export const switchAndClear = (tags: Tag[], idx: number, imageList: ImageListType) => {
    switchTag(tags, idx)
    clearImageList(imageList)
}

export function addAndSwitchAndClear(tags: Tag[], idx: number, imageList: ImageListType) {
    addTag(tags, idx)
    switchAndClear(tags, idx, imageList)
}
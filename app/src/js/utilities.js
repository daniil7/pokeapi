
// 
// Array helpers

Array.prototype.filterStringFieldIncludes = function (
    field,
    target_value
) {
    return this.filter((value) => {
        return value[field]
              .replace(/ /g, '')
              .toLowerCase()
              .includes(target_value.replace(/ /g, '').toLowerCase());
    });
}

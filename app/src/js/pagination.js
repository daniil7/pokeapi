export default class Pagination 
{
    constructor(one_page_limit)
    {
        this.current_page = 0;
        this.one_page_limit = one_page_limit;
        this.pages_count = 0;
    }

    paginate(data) {
        this.pages_count = Math.ceil(
            data.length / this.one_page_limit
        );
        if (this.current_page >= this.pages_count)
            this.current_page = 0;
        let paginated = data.slice(
            this.current_page * this.one_page_limit,
            (this.current_page+1) * this.one_page_limit
        );
        return paginated;
    }
}

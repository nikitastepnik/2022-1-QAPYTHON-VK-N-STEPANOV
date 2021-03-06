import re


class InvalidSeparateRequests(Exception):
    pass


class BaseParser:
    def __init__(self, file):
        self.file = file
        self.nginx_log = open(self.file)
        self.total_requests = 0
        self.total_count_get_requests = 0
        self.total_count_post_requests = 0
        self.total_count_put_requests = 0
        self.total_count_patch_requests = 0
        self.total_count_delete_requests = 0
        self.total_count_copy_requests = 0
        self.total_count_head_requests = 0
        self.total_count_options_requests = 0
        self.total_count_link_requests = 0
        self.total_count_unlink_requests = 0
        self.total_count_purge_requests = 0
        self.total_count_lock_requests = 0
        self.total_count_unlock_requests = 0
        self.total_count_view_requests = 0
        self.total_count_propfind_requests = 0

    def reopen_file(self):
        self.nginx_log.seek(0)

    def close_file(self):
        self.nginx_log.close()

    def count_total_number_of_requests(self):
        http_methods = ['"GET ', '"POST ', '"PUT ', '"PATCH ', '"DELETE ', '"COPY ', '"HEAD ', '"OPTIONS ',
                        '"LINK ', '"UNLINK ', '"PURGE ', '"LOCK ', '"UNLINK ', '"PURGE ', '"LOCK ',
                        '"UNLOCK ', '"PROPFIND ', '"VIEW ']
        for line in self.nginx_log:
            for iter in http_methods:
                if iter in line:
                    self.total_requests += 1

        self.reopen_file()
        return self.total_requests

    def count_total_requests_separate_by_type(self):
        count_requests_separated_by_type_dict = {"GET": self.total_count_get_requests,
                                                 "POST": self.total_count_post_requests,
                                                 "PUT": self.total_count_put_requests,
                                                 "DELETE": self.total_count_delete_requests,
                                                 "PATCH": self.total_count_patch_requests,
                                                 "OPTIONS": self.total_count_options_requests,
                                                 "HEAD": self.total_count_head_requests,
                                                 "LINK": self.total_count_link_requests,
                                                 "UNLINK": self.total_count_unlink_requests,
                                                 "PURGE": self.total_count_purge_requests,
                                                 "LOCK": self.total_count_lock_requests,
                                                 "UNLOCK": self.total_count_unlock_requests,
                                                 "PROPFIND": self.total_count_unlink_requests,
                                                 "VIEW": self.total_count_view_requests}

        for line in self.nginx_log:
            for key in count_requests_separated_by_type_dict.keys():
                if '"' + key + " " in line:
                    count_requests_separated_by_type_dict[key] = count_requests_separated_by_type_dict[key] + 1 if \
                        count_requests_separated_by_type_dict.get(key) else 1

        self.reopen_file()
        if self.check_correct_separated(count_requests_separated_by_type_dict):
            return count_requests_separated_by_type_dict
        else:
            raise InvalidSeparateRequests("Sum of requests separated by type is not equal to the total number"
                                          "of requests")

    def check_correct_separated(self, count_requests_separated_by_type_dict):
        requests_values = count_requests_separated_by_type_dict.values()
        summary_count_requests = 0

        for value in requests_values:
            summary_count_requests += value

        if summary_count_requests == self.total_requests:
            return True
        else:
            return False

    def top_ten_requests_by_usage(self):
        urls_by_usage = {}
        delimiters = ["%", "?", "#"]
        for line in self.nginx_log:
            url = line.split(" ")[6]
            for sep in delimiters:
                if sep in url:
                    url = url.split(sep)[0]

            if url in urls_by_usage.keys():
                urls_by_usage[url] += 1
            else:
                urls_by_usage[url] = 1

        list_requests = list(urls_by_usage.items())
        list_requests.sort(key=lambda url: url[1], reverse=True)

        top_ten_requests_by_usage = list_requests[0:10]

        self.reopen_file()

        return top_ten_requests_by_usage

    def top_five_biggest_requests_ended_client_error(self):
        urls_by_usage = {}
        for line in self.nginx_log:
            code = line.split(" ")[8]
            if re.match("4\d\d", code):
                url = line.split(" ")[6]
                response_size = line.split(" ")[9]
                ip_address = line.split(" ")[0]
                key = url + " " + code + " " + ip_address
                if (key in urls_by_usage.keys()) and (int(response_size) > int(urls_by_usage[key])):
                    urls_by_usage[key] = int(response_size)
                elif key not in urls_by_usage.keys():
                    urls_by_usage[key] = int(response_size)

        list_requests = list(urls_by_usage.items())
        list_requests.sort(key=lambda url: url[1], reverse=True)

        top_biggest_requests_ended_client_error = list_requests[0:5]

        self.reopen_file()

        return top_biggest_requests_ended_client_error

    def top_five_users_by_count_of_requests_ended_server_error(self):
        urls_by_usage = {}
        for line in self.nginx_log:
            code = line.split(" ")[8]
            if re.match("5\d\d", code):
                ip_address = line.split(" ")[0]
                if ip_address in urls_by_usage.keys():
                    urls_by_usage[ip_address] += 1
                else:
                    urls_by_usage[ip_address] = 1

        list_requests = list(urls_by_usage.items())
        list_requests.sort(key=lambda url: url[1], reverse=True)

        top_users_by_count_of_requests_ended_server_error = list_requests[0:5]

        self.close_file()

        return top_users_by_count_of_requests_ended_server_error

import sys

def main():
    descriptions = ["user_info_8","user_info_4","user_info_3","user_info_2","serps_without_clicks_0","queries_wo_clicks_in_top_0","queries_count_1","queries_count_0","avg_time_between_click_to_query_2","user_info_7","user_info_1","user_info_0","uniq_click","switch_2","first_click_2","click_on_urls_9","click_count_1","click_count_0","avg_time_between_click_to_query_0","avg_click_on_urls_0","user_info_6","switch_1","session_duration_0","click_on_urls_8","avg_clicked_serps_2"]
    line_index = 0
    for line in sys.stdin:
        line_index += 1
        s = line.strip().split('\t')
        if s[0] in descriptions:
            print line_index


if __name__ == '__main__':
    main()

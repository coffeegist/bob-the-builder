import sys

class Menu:

    @staticmethod
    def choose_from_list(items, item_type="item", field="name"):
        while True:
            try:
                print()
                for index, item in enumerate(items, start=1):
                    if field is None:
                        item_title = item
                    else:
                        item_title = getattr(item, field)
                    print("{0} - {1}".format(index, item_title))

                if len(items) == 1:
                    selection = 1
                else:
                    selection = int(input("\nChoose {} number (0 to quit): ".format(item_type)))
                if selection <= len(items) and selection > 0:
                    return items[selection - 1]
                elif selection == 0:
                    sys.exit(0)
            except KeyboardInterrupt:
                sys.exit(0)
            except ValueError:
                print("Invalid selection.")


    @staticmethod
    def choose_multiple_from_list(items, item_type="item", field="name"):
        selected_items = []

        while True:
            try:
                print()
                for index, item in enumerate(items, start=1):
                    if field is None:
                        item_title = item
                    else:
                        item_title = getattr(item, field)
                    print("{0} - {1}".format(index, item_title))

                if len(items) == 1:
                    selections = ['1']
                else:
                    selections = input("\nChoose multiple comma-separated {} numbers (0 to quit): ".format(item_type))

                for selection in selections.split(','):
                    selection = int(selection)
                    if selection <= len(items) and selection > 0:
                        selected_items.append(items[selection - 1])
                    elif selection == 0:
                        sys.exit(0)

                return selected_items
            except KeyboardInterrupt:
                sys.exit(0)
            except ValueError:
                print("Invalid selection.")


    @staticmethod
    def yes_or_no(question):
        result = True

        reply = str(input(question+' (Y/n): ')).lower().strip()

        if len(reply) > 0 and reply[0] == 'n':
            result = False

        return result

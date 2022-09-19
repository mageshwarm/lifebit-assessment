###
# RULE SET THAT KEEPS PACKAGE'S DEPENDENCIES AND CONFLICTS
###
class RuleSet():
    def __init__(self) -> None:
        self.pkgs = dict()
        self.conflicts = []

    ###
    # ADD PACKAGE DEPENDENCY
    ###
    def addDep(self, pkg1: str, pkg2: str):
        pkgList = self.pkgs.get(pkg1, [])
        if pkg1 != pkg2:
            pkgList.append(pkg2)
        self.pkgs[pkg1] = pkgList


    ###
    # ADD PACKAGE CONFLICTS
    ###
    def addConflict(self, pkg1: str, pkg2: str):
        self.conflicts.append((pkg1, pkg2))


    ###
    # RETURN RULESET IS COHERENT
    ###
    def isCoherent(self):
        for x in self.pkgs.keys():
            val = self.getDeps(x, [])
            if self.___isConflict(val):
                return False
        return True


    ###
    # GET DEPENDENCY DAG FOR GIVEN PACKAGE
    ###
    def getDeps(self, pkg: str, result: list):
        result.append(pkg)
        for x in self.pkgs.get(pkg, []):
            if x not in result:
                self.getDeps(x, result)
            else:
                break
        return result


    ###
    # RETURN CONFLICTS BY CHECKING CONFLICTS VAR IS EXISTS IN BOTH RESULT AND VAL.
    ###
    def ___isConflict(self, val: list):
        for conflict in self.conflicts:
            # if both conflicts (src, dest pkgs) are exists in same list, it is not valid one.
            if all(x in val for x in [conflict[0], conflict[1]]):
                return True
        return False


###
# PACKAGE MANAGER CLASS
###
class Pkgs():
    def __init__(self, rs: RuleSet) -> None:
        self.rs = rs
        self.selectedPackages = list()


    ###
    # ADD GIVEN PACKAGE IF NOT EXISTS. IF EXISTS, REMOVE IT.
    ###
    def toggle(self, pkg: str):
        if pkg in self.selectedPackages: # if package is already selected, delete it.
            self.selectedPackages.remove(pkg)
        else: # add pkg with list of dependencies
            self.selectedPackages.append(pkg)


    ###
    #  RETURN SELECTION OF PACKAGES WITHOUT CONFLICTS
    ###
    def selection(self):
        reverseOrdered = self.selectedPackages[::-1]
        result = set()
        for sPkg in reverseOrdered:
            val = self.rs.getDeps(sPkg, [])
            
            # IF NO CONFLICTS, ADD PKGs TO RESULT
            if not self.___isConflict(result, val):
                result.update(val)

            # if selected item is not part of result due to conflicts, remove it from selectedPackages
            if sPkg not in result:
                self.selectedPackages.remove(sPkg)

        return result


    ###
    # RETURN CONFLICTS BY CHECKING CONFLICTS VAR IS EXISTS IN BOTH RESULT AND VAL.
    ###
    def ___isConflict(self, result: list, val: list):
        for conflict in self.rs.conflicts:
            # if both conflicts should exists in result and val, we shouldnt add val into result.
            if any(x in val for x in [conflict[0], conflict[1]]) and any(x in result for x in [conflict[0], conflict[1]]):
                return True
        return False

